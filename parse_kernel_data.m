function [time, y, y_est, uc, u, v,...
                theta, R, S, T, D, P, phi_P_phi] = parse_kernel_data(path)
    time = [];
    y = [];
    y_est = [];
    uc = [];
    u = [];
    v = [];
    theta = [];
    R = [];
    S = [];
    T = [];
    D = [];
    P = [];
    phi_P_phi = [];

    lines = get_lines(path);
    for i = 1:numel(lines)
        line = get_line_vectors(lines(i));
        time = [time; double(line(1)) + double(line(2))/1000000000];
        y = [y; double(line(4))];
        y_est = [y_est; double(line(5))];
        uc = [uc; double(line(6))];
        u = [u; double(line(7))];
        v = [v; double(line(8))];
        theta = [theta; double(get_vector_elements(line(9)))];
        R = [R; double(get_vector_elements(line(10)))];
        S = [S; double(get_vector_elements(line(11)))];
        T = [T; double(get_vector_elements(line(12)))];
        D = [D; double(get_vector_elements(line(13)))];
        P = [P; double(get_vector_elements(line(14)))];
        phi_P_phi = [phi_P_phi; double(line(15))];
    end
end

function lines = get_lines(path)
    filestr = fileread(path);
    filestr = erase(filestr, '[');
    filestr = erase(filestr, ']');
    filestr = native2unicode(filestr);
    % %break it into lines
    filebyline = regexp(filestr, '\n', 'split');
    % % %remove empty lines
    filebyline( cellfun(@isempty,filebyline) ) = [];
    lines = convertCharsToStrings(filebyline);
end

function line_vectors = get_line_vectors(line)
   linebyvectors = regexp(line, ';', 'split');
   line_vectors = convertCharsToStrings(linebyvectors);
end

function vector_elements = get_vector_elements(vector)
    vectorbyelements = regexp(vector, ',', 'split');
    vector_elements = vectorbyelements;
end
